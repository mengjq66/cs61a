
; Tail recursion

(define (replicate x n)
  (define (tail-replicate k r)
    (if (= k n)
        r
        (tail-replicate (+ k 1) (cons x r))))
  (tail-replicate 0 nil)
)

(define (accumulate combiner start n term)
  (if (= n 0)
      start
      (accumulate combiner (combiner start (term n)) (- n 1) term)
  )
)

(define (accumulate-tail combiner start n term)
  (if (= n 0)
      start
      (accumulate combiner (combiner start (term n)) (- n 1) term)
  )
)

; Streams

(define (map-stream f s)
    (if (null? s)
    	nil
    	(cons-stream (f (car s)) (map-stream f (cdr-stream s)))))

(define multiples-of-three
  (cons-stream 3 (map-stream (lambda (x) (+ x 3)) multiples-of-three))
)



(define (nondecreastream s)
  (cond ((null? s) nil)
    ((or (null? (cdr-stream s))
         (< (car (cdr-stream s)) (car s)))
         (cons-stream (cons (car s) nil)
                      (nondecreastream (cdr-stream s)))
    )
    (else
      (let ((rest-strm (nondecreastream (cdr-stream s))))
           (cons-stream (cons (car s) (car rest-strm)) (cdr-stream rest-strm))
      )
    )
  )
)


(define finite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 3
                (cons-stream 1
                    (cons-stream 2
                        (cons-stream 2
                            (cons-stream 1 nil))))))))

(define infinite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 2
                infinite-test-stream))))