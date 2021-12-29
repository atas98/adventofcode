use std::fs::File;
use std::io::{BufRead, BufReader, Result};

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let reader = BufReader::new(input_file);

    let mut res: u32 = 0;
    reader
        .lines()
        .map(|val| val.unwrap().parse::<u32>().unwrap())
        .fold((9999, 9999, 9999), |acc, x| {
            if acc.1 + acc.2 + x > acc.0 + acc.1 + acc.2 {
                res += 1;
            }
            (acc.1, acc.2, x)
        });
        println!("{}", res);

    Ok(())
}
