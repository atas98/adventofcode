use std::fs::File;
use std::io::{BufRead, BufReader, Result};

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let reader = BufReader::new(input_file);

    let moves: Vec<_> = reader
        .lines()
        .map(|s| s.unwrap().split(' ').map(str::to_owned).collect::<Vec<_>>())
        .collect();

    let mut vertical = 0;
    let mut horizontal = 0;

    for line in moves {
        let dir = &line[0];
        let dist: i32 = line[1].parse::<i32>().unwrap();

        match dir.as_str() {
            "forward" => {
                horizontal += dist;
            }
            "up" => {
                vertical -= dist;
            }
            "down" => {
                vertical += dist;
            }
            _ => {
                unreachable!()
            }
        }
    }

    println!("{} {} {}", horizontal, vertical, horizontal * &vertical);

    Ok(())
}
