import struct
import zlib

def make_chunk(tag, body):
    crc = zlib.crc32(tag + body) & 0xFFFFFFFF
    return struct.pack(">I", len(body)) + tag + body + struct.pack(">I", crc)

def fix(src="challenge.png", dst="fixed.png"):
    d = open(src, "rb").read()

    # rebuild the header with the correct size
    ihdr = make_chunk(b"IHDR", struct.pack(">IIBBBBB", 724, 850, 8, 2, 0, 0, 0))

    # chunk 2 has 12 junk bytes injected, so cut them out and redo its CRC
    body = d[131137:196685]
    idat2 = make_chunk(b"IDAT", body[:7240] + body[7252:])

    fixed = (
        d[:8] + ihdr
        + d[33:33 + 65548]
        + d[65581:65581 + 65548]
        + idat2
        + d[196689:196689 + 65548]
        + d[262237:262237 + 65548]
        + d[327785:327785 + 65548]
        + d[393333:393333 + 21798]
        + d[415131:]
    )

    open(dst, "wb").write(fixed)
    print(f"Fixed image saved to {dst}")

fix()