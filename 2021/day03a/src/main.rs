use std::fs::File;
use std::io::{BufRead, BufReader, Result};

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let reader = BufReader::new(input_file);

    let lines: Vec<_> = reader
        .lines()
        .map(|s| {
            s.unwrap()
                .chars()
                .flat_map(|c| c.to_digit(2))
                .collect::<Vec<_>>()
        })
        .collect();

    let input_half = lines.len() / 2;
    let line_len = lines[0].len();
    let (gamma_rate, epsilon_rate) = lines
        .iter()
        .fold(vec![0; line_len], |acc, line| {
            acc.iter().zip(line.iter()).map(|(&a, &b)| a + b).collect()
        })
        .iter()
        .map(|&d| {
            (
                ((d > input_half as u32) as u32),
                ((d < input_half as u32) as u32),
            )
        })
        .fold((0, 0), |acc, b| {
            (acc.0 * 2 + b.0 as u32, acc.1 * 2 + b.1 as u32)
        });

    println!(
        "{} {} {}",
        gamma_rate,
        epsilon_rate,
        gamma_rate * epsilon_rate
    );

    Ok(())
}
