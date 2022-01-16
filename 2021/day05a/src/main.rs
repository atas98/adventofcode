use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Result};

#[derive(PartialEq, Eq, Hash, Debug)]
struct Point {
    x: usize,
    y: usize,
}

fn count_intersections<T>(lines: T) -> usize
where
    T: Iterator<Item = Result<String>>,
{
    let mut coords: Vec<Vec<usize>>;
    let mut map: HashMap<Point, usize> = HashMap::new();

    for line in lines {
        coords = line
            .unwrap()
            .split(" -> ")
            .map(|pair| {
                pair.split(",")
                    .map(|el| el.parse::<usize>().unwrap())
                    .collect::<Vec<usize>>()
            })
            .collect::<Vec<Vec<usize>>>();

        if coords[0][0] == coords[1][0] {
            for y in coords[0][1].min(coords[1][1])..coords[0][1].max(coords[1][1]) + 1 {
                if let Some(&val) = map.get(&Point {
                    x: coords[0][0],
                    y: y,
                }) {
                    map.insert(
                        Point {
                            x: coords[0][0],
                            y: y,
                        },
                        val + 1,
                    );
                } else {
                    map.insert(
                        Point {
                            x: coords[0][0],
                            y: y,
                        },
                        1,
                    );
                }
            }
        } else if coords[0][1] == coords[1][1] {
            for x in coords[0][0].min(coords[1][0])..coords[0][0].max(coords[1][0]) + 1 {
                if let Some(&val) = map.get(&Point {
                    x: x,
                    y: coords[0][1],
                }) {
                    map.insert(
                        Point {
                            x: x,
                            y: coords[0][1],
                        },
                        val + 1,
                    );
                } else {
                    map.insert(
                        Point {
                            x: x,
                            y: coords[0][1],
                        },
                        1,
                    );
                }
            }
        }
    }
    map.into_iter().filter(|(_, v)| *v > 1).count()
}

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let reader = BufReader::new(input_file);

    let lines = reader.lines();

    println!("{:?}", count_intersections(lines));

    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::count_intersections;

    #[test]
    fn test_data() {
        let data = vec![
            "0,9 -> 5,9".to_string(),
            "8,0 -> 0,8".to_string(),
            "9,4 -> 3,4".to_string(),
            "2,2 -> 2,1".to_string(),
            "7,0 -> 7,4".to_string(),
            "6,4 -> 2,0".to_string(),
            "0,9 -> 2,9".to_string(),
            "3,4 -> 1,4".to_string(),
            "0,0 -> 8,8".to_string(),
            "5,5 -> 8,2".to_string(),
        ];

        let res = count_intersections(data.into_iter().map(|el| Ok(el)));
        println!("{}", res);
        assert_eq!(res, 5);
    }
}
