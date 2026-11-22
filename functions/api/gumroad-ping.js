// Gumroad "Ping" webhook. Gumroad POSTs every sale here (form-encoded).
// The ping URL in Gumroad settings must carry the shared secret, e.g.
//   https://keepseeingnumbers.com/api/gumroad-ping?secret=<PING_SECRET>
// We store the sale under the checkout session id (sid) that the site adds
// to the product link, so /api/claim can hand the license key back to the
// buyer's browser without them copying it from the receipt.

const SID_RE = /^[a-f0-9]{24}$/;

function secretFrom(request, url) {
  return (
    url.searchParams.get("secret") ||
    url.searchParams.get("key") ||
    url.searchParams.get("token") ||
    request.headers.get("x-ping-secret") ||
    ""
  );
}

function safeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  if (!env.PING_SECRET || !safeEqual(secretFrom(request, url), env.PING_SECRET)) {
    return new Response("forbidden", { status: 403 });
  }
  let form;
  try {
    form = await request.formData();
  } catch (e) {
    return new Response("bad request", { status: 400 });
  }
  const get = (k) => (form.get(k) || "").toString();
  const sid = (get("url_params[sid]") || get("sid")).toLowerCase();
  const licenseKey = get("license_key");
  const record = {
    license_key: licenseKey,
    sale_id: get("sale_id"),
    product_id: get("product_id"),
    refunded: get("refunded") === "true",
    test: get("test") === "true",
    t: Date.now(),
  };
  if (env.SALES && licenseKey) {
    const ttl = 60 * 60 * 24 * 7;
    if (SID_RE.test(sid)) {
      await env.SALES.put("sid:" + sid, JSON.stringify(record), { expirationTtl: ttl });
    }
    if (record.sale_id) {
      await env.SALES.put("sale:" + record.sale_id, JSON.stringify(Object.assign({ sid }, record)));
    }
  }
  return new Response("ok", { status: 200 });
}
