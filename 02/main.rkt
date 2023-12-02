#lang racket
(require predicates)

(define GAME-REGEX (pregexp "Game (\\d+)"))
(define RGB-VALUE-REGEX (pregexp "(\\d+) (red|green|blue)"))

(struct rgb-set (red green blue) #:transparent)

(define (rgb-set-map fn)
  (λ (set-a set-b)
    (rgb-set (fn (rgb-set-red set-a) (rgb-set-red set-b))
             (fn (rgb-set-green set-a) (rgb-set-green set-b))
             (fn (rgb-set-blue set-a) (rgb-set-blue set-b)))))

(define rgb-set-add (rgb-set-map +))

(define rgb-set-max (rgb-set-map max))

(define (rgb-set-max-of rgbs)
  (foldl (λ (rgb acc)
           (rgb-set-max acc rgb))
         (rgb-set 0 0 0)
         rgbs))

(define (rgb-set-power rgb)
  (* (rgb-set-red rgb)
     (rgb-set-green rgb)
     (rgb-set-blue rgb)))

(struct game (id rgb-sets) #:transparent)

(define (parse-rgb-value s)
  (let* ([matches (regexp-match RGB-VALUE-REGEX s)]
         [cnt (string->number (cadr matches))]
         [color (caddr matches)])
    (cond
      [(string=? color "red") (rgb-set cnt 0 0)]
      [(string=? color "green") (rgb-set 0 cnt 0)]
      [(string=? color "blue") (rgb-set 0 0 cnt)])))

(define (parse-rgb-set s)
  (let ([values (string-split s ",")])
    (foldl (λ (value-str acc)
             (rgb-set-add acc (parse-rgb-value value-str)))
           (rgb-set 0 0 0)
           values)))

(define (parse-rgb-sets s)
  (let ([sets (string-split s ";")])
    (map parse-rgb-set sets)))

(define (parse-game-id s)
  (string->number (list-ref (regexp-match GAME-REGEX s) 1)))

(define (parse-game line)
  (let* ([segments (string-split line ":")]
         [game-str (car segments)]
         [sets-str (cadr segments)]
         [id (parse-game-id game-str)]
         [rgb-sets (parse-rgb-sets sets-str)])
    (game id rgb-sets)))

(define (rgb-set-valid? rgb)
  (and (<= (rgb-set-red rgb) 12)
       (<= (rgb-set-green rgb) 13)
       (<= (rgb-set-blue rgb) 14)))

(define (game-valid? g)
  ((all? rgb-set-valid?) (game-rgb-sets g)))

(define (sum-ids-of-valid-games lines)
  (apply +
         (map game-id
              (filter game-valid?
                      (map parse-game
                           lines)))))

(define (sum-of-powers lines)
  (let* ([games (map parse-game lines)]
         [max-rgbs (map rgb-set-max-of (map game-rgb-sets games))]
         [powers (map rgb-set-power max-rgbs)])
    (apply + powers)))
    

(with-input-from-file "input.txt"
  (λ ()
    (writeln (sum-of-powers (sequence->list (in-lines))))))
