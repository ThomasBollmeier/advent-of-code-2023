#lang racket

(define (parse-numbers line)
  (let* ([matches (regexp-match* #px"(\\d+)" line)]
         [numbers (map string->number matches)])
    numbers))

(define (parse-races lines)
  (let ([times (parse-numbers (car lines))]
        [distances (parse-numbers (cadr lines))])
    (map (λ (t d) (list t d)) times distances)))

(define (max-distance load-time total-time)
  (* load-time (- total-time load-time)))

(define (num-winning race)
  (let* ([duration (car race)]
         [previous-win-dist (cadr race)]
         [load-times (range duration)])
    (length (filter (λ (t) (> (max-distance t duration)
                            previous-win-dist))
                    load-times))))

(define (part1 lines)
  (let ([races (parse-races lines)])
    (writeln (apply * (map num-winning races)))))

(define (parse-number-2 line)
  (let* ([matches (regexp-match* #px"(\\d+)" line)])
    (string->number (apply string-append matches))))

(define (parse-race-2 lines)
  (let ([time (parse-number-2 (car lines))]
        [distance (parse-number-2 (cadr lines))])
    (list time distance)))

;; (x - t/2)^2 < t^2/4 - d
;; x < t/2 + 1/2 (t^2 - 4d)^(1/2) oder
;; x > t/2 - 1/2 (t^2 - 4d)^(1/2)
(define (num-winning-2 race)
  (let* ([t (car race)]
         [d (cadr race)]
         [valid? (λ (x) (not (zero? (- (* (- t x) x) d))))]
         [y (sqrt (- (sqr t) (* 4 d)))]
         [xmax (exact-floor (+ (/ t 2) (/ y 2)))]
         [xmax (if (valid? xmax) xmax (sub1 xmax))]
         [xmin (exact-ceiling (- (/ t 2) (/ y 2)))]
         [xmin (if (valid? xmin) xmin (add1 xmin))])
    (add1 (- xmax xmin))))

(define (part2 lines)
  (writeln (num-winning-2 (parse-race-2 lines))))

(with-input-from-file "input.txt"
  (λ ()
    (part2 (sequence->list (in-lines)))))
