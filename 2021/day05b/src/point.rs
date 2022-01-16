use std::ops::{Sub, Add, Mul, Div};

#[derive(PartialEq, Eq, Hash, Debug, Clone, Copy)]
pub struct Point {
    pub x: isize,
    pub y: isize,
}

pub fn new<T>(iter: &mut T) -> Point
where T: Iterator<Item = isize> {
    Point {
        x: iter.next().unwrap(),
        y: iter.next().unwrap(),
    }
}

pub trait Normalize {
    type Output;
    fn to_unit(&self) -> Self::Output;
}

impl Sub for Point {
    type Output = Self;

    fn sub(self, other: Self) -> Self::Output {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl Add for Point {
    type Output = Self;

    fn add(self, other: Self) -> Self::Output {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Add<Point> for &Point {
    type Output = Point;

    fn add(self, other: Point) -> Self::Output {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Add<Point> for &mut Point {
    type Output = Point;

    fn add(self, other: Point) -> Self::Output {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Mul<isize> for Point {
    type Output = Self;

    fn mul(self, other: isize) -> Self::Output {
        Self {
            x: self.x * other,
            y: self.y * other,
        }
    }
}

impl Div for Point {
    type Output = Self;

    fn div(self, other: Self) -> Self::Output {
        Self {
            x: self.x / other.x,
            y: self.y / other.y,
        }
    }
}

impl Normalize for Point {
    type Output = Self;

    fn to_unit(&self) -> Self::Output {
        Self {
            x: self.x.signum(),
            y: self.y.signum(),
        }
    }
}
