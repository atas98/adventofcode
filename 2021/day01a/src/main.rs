use std::fs::File;
use std::io::{BufRead, BufReader, Result};

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let reader = BufReader::new(input_file);

    let mut res: u32 = 0;
    reader
        .lines()
        .map(|val| val.unwrap().parse::<u32>().unwrap())
        .fold(u32::MAX, |acc, x| {
            if x > acc {
                res += 1;
            }
            x
        });
        println!("{}", res);

    Ok(())
}
