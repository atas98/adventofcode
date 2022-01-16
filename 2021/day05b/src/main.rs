use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Result};

mod point;
use point::{Normalize, Point};

fn count_intersections<T>(lines: T) -> usize
where
    T: Iterator<Item = Result<String>>,
{
    let mut map: HashMap<Point, isize> = HashMap::new();

    for line in lines {
        let coords = line
            .unwrap()
            .split(" -> ")
            .map(|pair| {
                pair.split(",")
                    .map(|el| el.parse::<isize>().unwrap())
                    .collect::<Vec<isize>>()
            })
            .collect::<Vec<Vec<isize>>>();
        let (start, end) = (
            point::new(&mut coords[0].clone().into_iter()),
            point::new(&mut coords[1].clone().into_iter()),
        );

        if start.x == end.x {
            for y in start.y.min(end.y)..start.y.max(end.y) + 1 {
                if let Some(&val) = map.get(&Point { x: start.x, y: y }) {
                    map.insert(Point { x: start.x, y: y }, val + 1);
                } else {
                    map.insert(Point { x: start.x, y: y }, 1);
                }
            }
        } else if start.y == end.y {
            for x in start.x.min(end.x)..start.x.max(end.x) + 1 {
                if let Some(&val) = map.get(&Point { x: x, y: start.y }) {
                    map.insert(Point { x: x, y: start.y }, val + 1);
                } else {
                    map.insert(Point { x: x, y: start.y }, 1);
                }
            }
        } else if (start.x - end.x).abs() == (start.y - end.y).abs() {
            let dir = (end - start).to_unit();
            let dist = (start.x - end.x).abs();
            for d in 0..dist + 1 {
                let new_point = start + (dir * d);
                if let Some(&val) = map.get(&new_point) {
                    map.insert(new_point, val + 1);
                } else {
                    map.insert(new_point, 1);
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
        assert_eq!(res, 12);
    }
}
