use std::fs::File;
use std::io::{BufRead, BufReader, Result};

// fn read_chunk(path: &str) -> Vec<Vec<usize>> {
// }

fn transpose<T>(v: Vec<Vec<T>>) -> Vec<Vec<T>> {
    assert!(!v.is_empty());
    let len = v[0].len();
    let mut iters: Vec<_> = v.into_iter().map(|n| n.into_iter()).collect();
    (0..len)
        .map(|_| {
            iters
                .iter_mut()
                .map(|n| n.next().unwrap())
                .collect::<Vec<T>>()
        })
        .collect()
}

fn check_win_condition_rows(marked: Vec<Vec<bool>>) -> bool {
    marked.iter().fold(false, |row_acc, row| {
        row.iter().fold(true, |el_acc, el| *el && el_acc) || row_acc
    })
}

fn check_win_condition(marked: &Vec<Vec<bool>>) -> bool {
    check_win_condition_rows(marked.clone()) || check_win_condition_rows(transpose(marked.clone()))
}

fn compute_score(board: &Vec<Vec<usize>>, marked: &Vec<Vec<bool>>, last_input: usize) -> usize {
    board
        .into_iter()
        .enumerate()
        .map(|(i, row)| {
            row.into_iter()
                .enumerate()
                .map(|(j, el)| if marked[i][j] { 0 } else { *el })
                .sum::<usize>()
        })
        .sum::<usize>()
        * last_input
}

fn simulate_for_board(board: &Vec<Vec<usize>>, inputs: &Vec<usize>) -> Option<(usize, Vec<Vec<bool>>)> {
    assert!(!board.is_empty());
    let mut marked = vec![vec![false; board[0].len()]; board.len()];
    for (turn, input) in inputs.iter().enumerate() {
        if let Some((i, j)) = board.iter().enumerate().fold(None, |acc, (i, row)| {
            if let Some(j) = row.iter().position(|el| el == input) {
                Some((i, j))
            } else {
                acc
            }
        }) {
            marked[i][j] = true;
            if check_win_condition(&marked) {
                return Some(((turn) as usize, marked));
            }
        }
    }
    None
}

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let mut lines = BufReader::new(input_file).lines();

    let inputs: Vec<usize> = lines
        .next()
        .unwrap()
        .unwrap()
        .split(",")
        .map(|el| el.parse::<usize>().unwrap())
        .collect();

    let mut res: Option<(Vec<Vec<usize>>, Vec<Vec<bool>>)> = None; // (turn, board, marked)
    let mut res_turn = inputs.len() + 1;

    let mut buf: Vec<Vec<usize>> = Vec::new();
    for line in lines {
        if let Ok(l) = line {
            if !l.is_empty() {
                buf.push(l
                    .split(" ")
                    .filter(|&el| !el.is_empty())
                    .map(|el| el.parse::<usize>().unwrap()
                ).collect());
                continue;
            }
            if !buf.is_empty() {
                if let Some((turn, marked)) = simulate_for_board(&buf, &inputs) {
                    if turn < res_turn {
                        res = Some((buf.clone(), marked.clone()));
                        res_turn = turn;
                    }
                }
                buf = Vec::new();
            }
        }
    }

    if let Some((board, marked)) = res {
        println!("The final score was: {}", compute_score(&board, &marked, inputs[res_turn]));
    } else {
        println!("There was no winners");
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn compute_score_test() {
        let board: Vec<Vec<usize>> = vec![
            vec![14, 21, 17, 24, 4],
            vec![10, 16, 15, 9, 19],
            vec![18, 8, 23, 26, 20],
            vec![22, 11, 13, 6, 5],
            vec![2, 0, 12, 3, 7],
        ];
        let marked: Vec<Vec<bool>> = vec![
            vec![true, true, true, true, true],
            vec![false, false, false, true, false],
            vec![false, false, true, false, false],
            vec![false, true, false, false, true],
            vec![true, false, false, false, true],
        ];
        let last_input: usize = 24;

        assert_eq!(compute_score(&board, &marked, last_input), 4512)
    }

    #[test]
    fn check_win_condition_rows_test() {
        assert_eq!(
            check_win_condition_rows(vec![
                vec![true, true, true, true, true],
                vec![false, false, false, true, false],
                vec![false, false, true, false, false],
                vec![false, true, false, false, true],
                vec![true, false, false, false, true],
            ]),
            true
        );
        assert_eq!(
            check_win_condition_rows(vec![
                vec![false, true, true, true, true],
                vec![false, false, false, true, false],
                vec![false, false, true, false, false],
                vec![false, true, false, false, true],
                vec![true, false, false, false, true],
            ]),
            false
        );
    }

    #[test]
    fn check_win_condition_test() {
        assert_eq!(
            check_win_condition(&vec![
                vec![true, true, true, true, true],
                vec![false, false, false, true, false],
                vec![false, false, true, false, false],
                vec![false, true, false, false, true],
                vec![true, false, false, false, true],
            ]),
            true
        );
        assert_eq!(
            check_win_condition(&vec![
                vec![true, false, true, true, true],
                vec![true, false, false, true, false],
                vec![true, false, true, false, false],
                vec![true, true, false, false, true],
                vec![true, false, false, false, true],
            ]),
            true
        );

        assert_eq!(
            check_win_condition(&vec![
                vec![true, false, true, true, true],
                vec![true, false, false, true, false],
                vec![false, false, true, false, false],
                vec![true, true, false, false, true],
                vec![true, false, false, false, true],
            ]),
            false
        );
    }

    #[test]
    fn simulate_for_board_test() {
        let board: Vec<Vec<usize>> = vec![
            vec![14, 21, 17, 24, 4],
            vec![10, 16, 15, 9, 19],
            vec![18, 8, 23, 26, 20],
            vec![22, 11, 13, 6, 5],
            vec![2, 0, 12, 3, 7],
        ];
        let inputs = vec![
            7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19,
            3, 26, 1,
        ];
        let marked: Vec<Vec<bool>> = vec![
            vec![true, true, true, true, true],
            vec![false, false, false, true, false],
            vec![false, false, true, false, false],
            vec![false, true, false, false, true],
            vec![true, true, false, false, true],
        ];

        assert_eq!(simulate_for_board(&board, &inputs), Some((11, marked)))
    }
}
