use std::{
    error::Error,
    fs::OpenOptions,
    io::{Read, Write},
};

use hex_simd::{AsciiCase, Out};
use md5::compute;

fn main() -> Result<(), Box<dyn Error>> {
    let mut save = OpenOptions::new().read(true).open("./save.json")?;
    let mut buf = Vec::new();
    save.read_to_end(&mut buf)?;

    let hash1 = compute(buf);
    let hash2 = compute(hash1.0);
    let hash3 = compute(hash2.0);

    let mut out_buf = [0u8; 32];
    let encoded = hex_simd::encode(&hash3.0, Out::from_slice(&mut out_buf), AsciiCase::Lower);

    let mut out = OpenOptions::new()
        .create(true)
        .write(true)
        .read(false)
        .open("./save.json.md5")?;
    out.write_all(&encoded)?;

    Ok(())
}
