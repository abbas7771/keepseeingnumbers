// Called by /report/ every few seconds after checkout:
//   GET /api/claim?sid=<24 hex chars>
// Returns {ready:true, license_key} once the Gumroad ping for that sid has
// arrived, otherwise {ready:false}.

const SID_RE = /^[a-f0-9]{24}$/;
const json = (obj, status) =>
  new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

export async function onRequestGet({ request, env }) {
  const sid = (new URL(request.url).searchParams.get("sid") || "").toLowerCase();
  if (!SID_RE.test(sid)) return json({ ready: false }, 400);
  if (!env.SALES) return json({ ready: false }, 200);
  const raw = await env.SALES.get("sid:" + sid);
  if (!raw) return json({ ready: false }, 200);
  let rec;
  try {
    rec = JSON.parse(raw);
  } catch (e) {
    return json({ ready: false }, 200);
  }
  if (!rec.license_key || rec.refunded) return json({ ready: false }, 200);
  return json({ ready: true, license_key: rec.license_key }, 200);
}
