use std::{
    error::Error,
    fs::OpenOptions,
    io::{Read, Seek, Write},
};

use hex_simd::{AsciiCase, Out};
use md5::compute;
use sonic_rs::Value;

fn main() -> Result<(), Box<dyn Error>> {
    println!("loading savedata...");
    let mut save = OpenOptions::new()
        .create(false)
        .read(true)
        .write(true)
        .open("save.json")?;

    let mut buf = Vec::new();
    save.read_to_end(&mut buf)?;

    let json: Value = sonic_rs::from_slice(&buf)?;
    let compact_json = sonic_rs::to_vec(&json)?;
    buf = compact_json;

    save.seek(std::io::SeekFrom::Start(0))?;
    save.set_len(0)?;
    save.write_all(&buf)?;

    println!("calculating hash...");
    let hash1 = compute(buf);
    let hash2 = compute(hash1.0);
    let hash3 = compute(hash2.0);

    let mut out_buf = [0u8; 32];
    let encoded = hex_simd::encode(&hash3.0, Out::from_slice(&mut out_buf), AsciiCase::Lower);

    println!("writing hash...");
    let mut out = OpenOptions::new()
        .create(true)
        .read(false)
        .write(true)
        .truncate(true)
        .open("save.json.md5")?;
    out.write_all(&encoded)?;

    println!("all done");
    Ok(())
}
