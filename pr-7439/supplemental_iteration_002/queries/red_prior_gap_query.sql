SELECT
  ingested_at,
  campaign_id,
  user_id,
  event_type,
  model,
  LENGTH(COALESCE(request_json, '')) AS request_len,
  LENGTH(COALESCE(response_text, '')) AS response_len,
  JSON_EXTRACT_SCALAR(extra_json, '$.path') AS path
FROM `worldarchitecture-ai.llm_forensics.llm_payloads`
WHERE event_type = 'gameplay_streaming_proxy'
  AND LENGTH(COALESCE(request_json, '')) = 0
ORDER BY ingested_at DESC
LIMIT 5;
