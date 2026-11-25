// Long films, rendered in chunks that survive interruption:
//   node core/render/chunks.mjs <film> [--fps 24] [--chunk 30] [--workers 3] [--out <film>/out/video.mp4]
//                                      [--only 1,7] [--redo 3,4] [--fresh] [--size 1920x1080] [--q 'k=v']
// The film is cut into chunks of --chunk seconds (default 30). Each chunk is rendered by video.mjs (--frames a:b) into
// <out>.chunks/c_0001.mp4 …, and its frame count checked. Finished chunks are kept: if the run stops (the session ends,
// the machine sleeps, a page error), run the same command again and it carries on from the first missing chunk.
// When every chunk is there, they are joined losslessly into --out and the total frame count is checked against DUR × fps.
//   --only 1,7   render just these chunks (numbered from 1) and stop without joining: a test render of the start and the middle
//   --redo 3,4   render these chunks again (after you changed the scenes they cover); --fresh starts over
// A chunk older than the newest source file in the film folder is listed as possibly stale; it is not re-rendered unless you --redo it.
import fs from 'fs'; import path from 'path'; import { spawn, spawnSync, execFileSync } from 'child_process'; import { fileURLToPath } from 'url';
import { openDemo, closeServer, requireDemo, takeSize } from './page.mjs';
const args = process.argv.slice(2), { w: W, h: H } = takeSize(args), opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const dir = path.resolve(args[0] || ''); requireDemo(dir);
const FPS = +opt('--fps', 24), CH = +opt('--chunk', 30), WK = opt('--workers', '3'), Q = opt('--q', '');
if (!(FPS > 0) || !(CH >= 2)) { console.error('bad --fps / --chunk: fps must be > 0, chunk at least 2 seconds'); process.exit(2); }
const nums = s => (s || '').split(',').filter(Boolean).map(Number);
const ONLY = nums(opt('--only')), REDO = new Set(nums(opt('--redo'))), FRESH = args.includes('--fresh');
const out = path.resolve(opt('--out', path.join(dir, 'out', 'video.mp4')));
const cdir = out.replace(/\.[^./]+$/, '') + '.chunks';
const HERE = path.dirname(fileURLToPath(import.meta.url));

// —— one run per chunk folder ——
const alive = pid => { if (!Number.isInteger(pid) || pid <= 0) return false; try { process.kill(pid, 0); return true; } catch (e) { return e.code === 'EPERM'; } };
if (FRESH) fs.rmSync(cdir, { recursive: true, force: true });
fs.mkdirSync(cdir, { recursive: true });
const lock = path.join(cdir, 'run.lock');
try { fs.writeFileSync(lock, String(process.pid), { flag: 'wx' }); } catch {
  const other = Number(fs.readFileSync(lock, 'utf8'));
  if (alive(other)) { console.error(`another chunk run (pid ${other}) is working in ${cdir}. Wait for it, or stop it first.`); process.exit(2); }
  fs.writeFileSync(lock, String(process.pid));
}
let child = null;
const unlock = () => { try { if (Number(fs.readFileSync(lock, 'utf8')) === process.pid) fs.unlinkSync(lock); } catch {} };
process.on('exit', unlock);
for (const sig of ['SIGINT', 'SIGTERM']) process.on(sig, () => { if (child) child.kill(sig); unlock(); process.exit(128 + (sig === 'SIGINT' ? 2 : 15)); });
const fail = msg => { console.error(msg); process.exit(1); };

// —— the film's length, and a manifest so chunks from different settings are never mixed ——
const probe = await openDemo(dir, { w: W, h: H, q: Q, gl: false }); const DUR = await probe.page.evaluate(() => window.DUR); await probe.browser.close(); closeServer();
if (!(DUR > 0)) fail(`window.DUR must be a positive number of seconds (got ${DUR})`);
const TOTAL = Math.round(DUR * FPS), CF = Math.round(CH * FPS), N = Math.ceil(TOTAL / CF);
const man = { dur: DUR, fps: FPS, size: `${W}x${H}`, q: Q, chunkFrames: CF, frames: TOTAL };
const manPath = path.join(cdir, 'manifest.json');
if (fs.existsSync(manPath)) {
  const old = JSON.parse(fs.readFileSync(manPath, 'utf8'));
  const diff = Object.keys(man).filter(k => String(old[k]) !== String(man[k]));
  if (diff.length) fail(`${cdir} holds chunks made with other settings (${diff.map(k => `${k}: ${old[k]} → ${man[k]}`).join(', ')}).\n` +
    `The film's length or settings changed, so the old chunks no longer line up. Run again with --fresh to start over.`);
} else fs.writeFileSync(manPath, JSON.stringify(man, null, 1));

// —— frame counting: ffprobe counts packets (fast); a build without ffprobe decodes the file instead ——
const frames = f => {
  try { const r = execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', path.basename(f)], { cwd: path.dirname(f), stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
    if (/^\d+$/.test(r)) return +r; } catch {}
  const err = String(spawnSync('ffmpeg', ['-nostdin', '-hide_banner', '-i', path.basename(f), '-map', '0:v:0', '-f', 'null', '-'], { cwd: path.dirname(f), encoding: 'utf8' }).stderr || '');
  const m = [...err.matchAll(/frame=\s*(\d+)/g)].pop(); return m ? +m[1] : -1;
};
const name = i => path.join(cdir, `c_${String(i).padStart(4, '0')}.mp4`);
const range = i => [(i - 1) * CF, Math.min(TOTAL, i * CF)];
const need = i => { const [a, b] = range(i); return b - a; };
const done = i => fs.existsSync(name(i)) && frames(name(i)) === need(i);

for (const i of [...ONLY, ...REDO]) if (!(Number.isInteger(i) && i >= 1 && i <= N)) fail(`chunk ${i} does not exist: the film has ${N} chunks of ${CH} s (1–${N})`);
for (const i of REDO) fs.rmSync(name(i), { force: true });

// —— chunks older than the newest source file ——
const newest = (() => { let t = 0; const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) {
  if (e.name.startsWith('.') || e.name === 'node_modules') continue; const p = path.join(d, e.name);
  if (p === path.dirname(out) || p === cdir || p.startsWith(path.join(dir, 'stills'))) continue;
  if (e.isDirectory()) walk(p); else if (/\.(m?js|html|json|css|glsl|frag|vert)$/.test(e.name)) t = Math.max(t, fs.statSync(p).mtimeMs);
} }; walk(dir); return t; })();
const stale = [...Array(N)].map((_, k) => k + 1).filter(i => fs.existsSync(name(i)) && fs.statSync(name(i)).mtimeMs < newest);
if (stale.length) console.log(`note: chunks ${stale.join(',')} are older than the newest source file. If your change touches them, run again with --redo ${stale.join(',')}.`);

// —— render what is missing ——
const todo = (ONLY.length ? ONLY : [...Array(N)].map((_, k) => k + 1)).filter(i => !done(i));
const mmss = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
console.log(`film ${DUR.toFixed(1)} s = ${TOTAL} frames at ${FPS} fps, ${N} chunks of ${CH} s; ${todo.length ? 'rendering chunks ' + todo.join(',') : 'nothing to render'}`);
const t0 = Date.now(); let made = 0, madeFrames = 0;
for (const i of todo) {
  const [a, b] = range(i), part = name(i).replace(/\.mp4$/, '.part.mp4');
  fs.rmSync(part, { force: true });
  const code = await new Promise(res => {
    child = spawn(process.execPath, [path.join(HERE, 'video.mjs'), dir, '--fps', String(FPS), '--workers', WK, '--frames', `${a}:${b}`, '--out', part, '--size', `${W}x${H}`, ...(Q ? ['--q', Q] : [])], { stdio: ['ignore', 'ignore', 'inherit'] });
    child.on('close', c => { child = null; res(c); });
  });
  if (code !== 0) fail(`chunk ${i} (${mmss(a / FPS)}–${mmss(b / FPS)}) failed (video.mjs's message is above). Fix it and run the same command again: finished chunks are kept.`);
  const got = frames(part);
  if (got !== b - a) fail(`chunk ${i} has ${got} frames instead of ${b - a}. Run the same command again to redo it.`);
  fs.renameSync(part, name(i)); made++; madeFrames += b - a;
  const el = (Date.now() - t0) / 1000, left = todo.slice(todo.indexOf(i) + 1).reduce((s, j) => s + need(j), 0);
  console.log(`chunk ${i}/${N} (${mmss(a / FPS)}–${mmss(b / FPS)}) ok  ${(madeFrames / el).toFixed(1)} frames/s, about ${mmss(left / (madeFrames / el))} left`);
}
if (ONLY.length) { console.log(`test chunks ${ONLY.join(',')} are in ${cdir}; nothing joined (--only)`); process.exit(0); }

// —— join ——
const list = path.join(cdir, 'list.txt');
fs.writeFileSync(list, [...Array(N)].map((_, k) => `file '${path.basename(name(k + 1))}'`).join('\n'));
const joined = path.join(cdir, 'joined.mp4');
try { execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'joined.mp4'], { cwd: cdir, stdio: ['ignore', 'inherit', 'inherit'] }); }
catch { fail('ffmpeg could not join the chunks (its message is above)'); }
const got = frames(joined);
if (got !== TOTAL) fail(`the joined film has ${got} frames instead of ${TOTAL}; the chunks are kept in ${cdir}`);
fs.mkdirSync(path.dirname(out), { recursive: true }); fs.renameSync(joined, out);
console.log(`done ${out}  ${TOTAL} frames (${mmss(DUR)}), ${made} chunks rendered this run. The chunks stay in ${cdir} until you delete it.`);
