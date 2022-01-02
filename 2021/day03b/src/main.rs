use std::fs::File;
use std::io::{BufRead, BufReader, Result};


fn vec_to_bin(line: &Vec<u32>) -> u32 {
    line.iter().fold(0, |acc, b| acc * 2 + *b)
}


fn filter_rating(lines: &Vec<Vec<u32>>, r_type: &str, eq_bit: u32) -> Option<u32> {
    let mut res = lines.clone();
    let line_len = lines[0].len();

    for i in 0..line_len {
        let input_half = (res.len() as f32 / 2.0).ceil() as u32;
        let bit_count = &res.clone().iter().map(|line| line[i]).sum::<u32>();
        let bit_filter = if *bit_count > input_half {
            match r_type {
                "oxygen" => 1,
                "co2" => 0,
                _ => panic!("Unexpected rating type!"),
            }
        } else if *bit_count < input_half {
            match r_type {
                "oxygen" => 0,
                "co2" => 1,
                _ => panic!("Unexpected rating type!"),
            }
        } else {
            eq_bit
    };
        res = res
            .iter()
            .filter(|line| line[i] == bit_filter)
            .cloned()
            .collect::<Vec<_>>();

        if res.len() == 1 {
            return Some(vec_to_bin(&res.clone()[0]));
        }
    }
    None
}


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

    if let Some(oxygen_rating) = filter_rating(&lines, "oxygen", 1) {
        if let Some(co2_rating) = filter_rating(&lines, "co2", 0) {
            println!("{}", oxygen_rating * &co2_rating);
        } else {
            println!("CO2 rating result is empty!")
        }
    } else {
        println!("Oxygen rating result is empty!")
    }

    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn vec_to_bin_test() {
        assert_eq!(
            vec_to_bin(&vec!(0, 0, 0)),
            0
        );
        assert_eq!(
            vec_to_bin(&vec!(1, 0, 1)),
            5
        );
        assert_eq!(
            vec_to_bin(&vec!(1, 0, 1, 0, 1, 0)),
            42
        );
    }

    #[test]
    fn filter_rating_test() {
        let test_data = vec![
            vec![0, 0, 1, 0, 0],
            vec![1, 1, 1, 1, 0],
            vec![1, 0, 1, 1, 0],
            vec![1, 0, 1, 1, 1],
            vec![1, 0, 1, 0, 1],
            vec![0, 1, 1, 1, 1],
            vec![0, 0, 1, 1, 1],
            vec![1, 1, 1, 0, 0],
            vec![1, 0, 0, 0, 0],
            vec![1, 1, 0, 0, 1],
            vec![0, 0, 0, 1, 0],
            vec![0, 1, 0, 1, 0],
        ];
        assert_eq!(filter_rating(&test_data, "oxygen", 1), Some(23));
        assert_eq!(filter_rating(&test_data, "co2", 0), Some(10));
    }
}
