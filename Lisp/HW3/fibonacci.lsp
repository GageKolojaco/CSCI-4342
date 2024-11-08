(defun fibonacci(n)
    (cond
        ((eq n 1) 0)
        ((eq n 2) 1)
        ((+ (fibonacci (- n 1)) (fibonacci (- n 2))))))
