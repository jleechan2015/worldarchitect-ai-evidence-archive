# INVALID — DO NOT USE AS EVIDENCE

This historical bundle is withdrawn. It predates the requested exact-head
validation and its checksum sidecars are intentionally no longer valid.

The real local-server and real-browser run at `10b17f7a599452feaed5191f31ca7776ef5e9d85`
reached the streaming endpoint but received zero provider chunks because AGY
reported quota exhaustion. No terminal SSE completion, stable during-stream
measurement, or after-completion measurement was captured. Do not treat any
following historical PASS claim as evidence.

# Historical bundle (invalid)

- **Branch**: `fix/streaming-scroll-anchor-keep-position`
- **Head SHA**: `284539f64882ab7922efb80ca041cfbf925a4c75`
- **Test**: Real-server browser streaming scroll preservation
- **Status**: ✅ **PASS (0.0px drift)**
