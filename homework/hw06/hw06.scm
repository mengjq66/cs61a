;;;;;;;;;;;;;;;
;; Questions ;;
;;;;;;;;;;;;;;;

; Scheme

(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cdr (cdr s)))
)

(define (sign x)
  (if (< x 0) -1 (if (= x 0) 0 1))
)

(define (square x) (* x x))

(define (pow b n)
  (if (= n 1) b (* b (pow b (- n 1))))
)

 (define (unique s)
  (if (null? s) '()
      (cons (car s)
      	(unique (filter (lambda (x) (not (equal? x (car s)))) (cdr s)))))
)