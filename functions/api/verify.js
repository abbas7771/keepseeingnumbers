// POST /api/verify  {license_key}
// Checks the key with Gumroad's license API before /report/ builds the report.
// Product id can be overridden with the GUMROAD_PRODUCT_ID variable.

const DEFAULT_PRODUCT_ID = "eKYznV4REYLKU-xWRMJsZw==";
const PERMALINK = "evpeqb";
const NOT_FOUND = "This license key wasn't recognised. Please copy it exactly from your Gumroad receipt.";

const json = (obj, status) =>
  new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

async function gumroadVerify(params) {
  const body = new URLSearchParams(Object.assign({ increment_uses_count: "false" }, params));
  const r = await fetch("https://api.gumroad.com/v2/licenses/verify", {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body,
  });
  let data = {};
  try {
    data = await r.json();
  } catch (e) {}
  return { status: r.status, data };
}

export async function onRequestPost({ request, env }) {
  let key = "";
  try {
    key = ((await request.json()).license_key || "").toString().trim();
  } catch (e) {}
  if (!key || key.length > 100) return json({ ok: false, error: NOT_FOUND }, 403);

  const productId = env.GUMROAD_PRODUCT_ID || DEFAULT_PRODUCT_ID;
  let res;
  try {
    res = await gumroadVerify({ product_id: productId, license_key: key });
    if (!res.data.success) {
      // fall back to the permalink for products made before product ids
      const alt = await gumroadVerify({ product_permalink: PERMALINK, license_key: key });
      if (alt.data.success) res = alt;
    }
  } catch (e) {
    return json({ ok: false, error: "Could not reach Gumroad. Please try again in a minute." }, 502);
  }
  const p = res.data && res.data.purchase;
  if (!res.data.success || !p) return json({ ok: false, error: NOT_FOUND }, 403);
  if (p.refunded || p.chargebacked || p.disputed) {
    return json({ ok: false, error: "This purchase was refunded, so the key no longer works." }, 403);
  }
  return json({ ok: true }, 200);
}
