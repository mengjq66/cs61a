(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.

(define (cons-all first rests)
  (map (lambda (x) (cons first x)) rests)
)

(define (zip pairs)
    (list (map car pairs) (map cadr pairs))
)

;; Problem 16
(define (enumerate s)
  ; BEGIN PROBLEM 16
  (define (help-enumerate s counter)
  ; (print (cdr s))
    (cond ((null? (cdr s)) (cons (list counter (car s)) nil)) (else 
    (cons (list counter (car s)) (help-enumerate (cdr s) (+ counter 1)))
    )))
  (if (null? s) nil 
  (help-enumerate s 0))
)
  ; END PROBLEM 16

;; Problem 17
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 17
  (cond
    ; if list is null, return nil
    ((null? denoms) nil)
    ; if number you're trying to partition to is 0, return (())
    ((<= total 0) (cons nil nil))
    ; if value in denoms is greater than total, skip it
    ((> (car denoms) total) (list-change total (cdr denoms)))
    (else
      ; append to car denoms with car and without car
      (append (cons-all (car denoms)
                 (list-change (- total (car denoms)) denoms))  ; with car, dont do cdr denoms since can be 1 1 1 1..
                 (list-change total (cdr denoms)))) ; without car
  )
  ; END PROBLEM 17
)

;; Problem 18
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 18
         expr
         ; END PROBLEM 18
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 18
         expr
         ; END PROBLEM 18
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 18
           (cons form (cons params (map let-to-lambda body))) ; evaluate the body with let-to-lambda
           ; END PROBLEM 18
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 18
           (begin (define vals (zip values))
                (cons (list 'lambda (let-to-lambda (car vals)) (car (let-to-lambda body)))
                      (let-to-lambda (cadr vals))))
           ; END PROBLEM 18
           ))
        (else
         ; BEGIN PROBLEM 18
         (map let-to-lambda expr)
         ; END PROBLEM 18
         )))
