#lang racket

(define (parse-node line)
  (let ([matches (regexp-match #px"([0-9A-Z]+)\\s*=\\s*\\(\\s*([0-9A-Z]+)\\s*,\\s*([0-9A-Z]+)\\s*\\)" line)])
    (cdr matches)))

(define (parse-route line)
  (let ([idx 0])
    (λ ()
      (let ([result (string-ref line idx)])
        (set! idx (modulo (add1 idx) (string-length line)))
        result))))

(define (parse-tree lines)
  (foldl (λ (line acc)
           (let* ([node-names (parse-node line)]
                  [key (car node-names)]
                  [children (cdr node-names)])
             (hash-set! acc key children)
             acc))
         (make-hash)
         lines))

(define (walk tree route start-state result end-fn? next-fn result-fn)
  (define (helper state result)
    (if (end-fn? state)
        result
        (let* ([direction (route)]
               [next-state (next-fn state direction)]
               [next-result (result-fn result)])
          (helper next-state next-result))))
  (helper start-state result))
        
(define (route-length tree route start end)
  (let ([end-fn? (lambda (state) (string=? state end))]
        [next-fn (lambda (state direction)
                    (let ([children (hash-ref tree state)])
                      (if (char=? direction #\L)
                          (car children)
                          (cadr children))))]
        [result-fn add1])
    (walk tree route start 0 end-fn? next-fn result-fn)))

(define (part1 lines)
  (let ([route (parse-route (car lines))]
        [tree (parse-tree (drop lines 2))])
    (writeln (route-length tree route "AAA" "ZZZ"))))

(define (last-char s)
  (string-ref s (sub1 (string-length s))))

(define (create-start-nodes tree)
  (filter (λ (s)
            (char=? (last-char s) #\A)) 
          (hash-keys tree)))

(define (create-next-node-fn tree)
  (λ (node direction)
    (let ([children (hash-ref tree node)])
      (if (char=? direction #\L)
          (car children)
          (cadr children)))))

(define (path-length tree route node)
  (walk tree 
        route 
        node
        0
        (λ (s) (char=? (last-char s) #\Z))
        (create-next-node-fn tree)
        add1))

(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (remainder a b))))

(define (lcm a b)
  (let ([c (gcd a b)])
    (* c (/ a c) (/ b c))))

(define (lcm* xs)
  (foldl (λ (x acc)
           (lcm x acc))
         1
         xs))
      
(define (part2 lines)
  (let* ([route-str (car lines)]
         [tree (parse-tree (drop lines 2))]
         [start-nodes (create-start-nodes tree)])
    (lcm* (map (λ (node)
                 (path-length tree
                              (parse-route route-str)
                              node)) 
               start-nodes))))
    
(with-input-from-file "input.txt"
  (λ ()
    (part2 (sequence->list (in-lines)))))
