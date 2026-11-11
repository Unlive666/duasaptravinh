// Netlify Serverless Function: Secure Proxy to Render Backend Gateway
// Zero secrets stored in repo — forwards directly to Render Cloud API!

const RENDER_API_URL = 'https://dua-sap-chatbot.onrender.com/api/web-order';

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ ok: false, error: 'Method Not Allowed' }) };
  }

  try {
    const res = await fetch(RENDER_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: event.body || '{}'
    });
    const text = await res.text();
    return {
      statusCode: res.status,
      headers,
      body: text
    };
  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ ok: false, error: 'Server error' }) };
  }
};
