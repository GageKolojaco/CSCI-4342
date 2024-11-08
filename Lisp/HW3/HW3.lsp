(defun read-polynomial (filename) ; declare function 
    (with-open-file (stream filename :if-does-not-exist nil)
        (let ((coefficients ())) ; declare modifiable list
            (loop for line = (read-line stream nil) ; update the line var to the next line on each loop
                while line  ; while the line var != nil
                do (let ((start 0)
                            (length (length line)))
                        (loop
                            while (< start length)
                            do (let ((comma (position #\, line :start start)))
                                (if comma
                                    (let ((number (subseq line start comma))) ; extract the substring from start to comma
                                    (push (parse-integer number) coefficients)
                                    (setf start (1+ comma))) ; move start to after the comma
                                    (progn
                                    (let ((number (subseq line start))) ; get the last number after the last comma
                                        (push (parse-integer number) coefficients))
                                    (setf start length) ; exit the loop
                                    )
                                )
                            )
                        )
                )
            )
            (nreverse coefficients) ; return coefficients in correct order
        )
    )
)

(defun polynomial (coefficients) ; declare function
    (let ((terms 
            (loop for coefficient in coefficients ; loop through list of coefficients
                  for exponent from 0 ; declare exponent var at 0 and begin action
                  when (/= coefficient 0)
                  collect 
                  (cond
                      ((= exponent 0)
                          (format nil "~a" coefficient)
                      ) 
                      ((= coefficient 1)
                          (format nil "x^~a" exponent)
                      )
                      (t
                          (format nil "~ax^~a" coefficient exponent)
                      )
                  )
            )
         ))
        (format nil "~{~a~^ + ~}" (reverse terms)) ; reverse terms to get proper order
    )
)

(defun eval-polynomial (coefficients x)
    (loop for coefficient in coefficients ; loop through list of coefficients
        for exponent from 0 ; declare exponent var at 0 and begin action
        sum (* coefficient (expt x exponent)) ; use sum to accumulate our calculated values, loop returns our final value       
    )
)

(defun main ()
    (let* ((coefficients (read-polynomial "poly_numbers.txt")) 
           (answer (polynomial coefficients)))
        (if coefficients 
            (progn
                (format t "Your polynomial is: ~a~%" answer) 
                (loop 
                    (format t "Enter a value for x (or type 'quit' to exit): ")
                    (let ((input (read-line)))
                        (cond 
                            ((string= input "quit")
                                (format t "Exiting program.~%")
                                (return)
                            )
                            ((handler-case 
                                 (parse-integer input)
                                 (error () nil))
                             (let ((x (parse-integer input)))
                                 (format t "Result: ~a~%" (eval-polynomial coefficients x))
                             )
                            )
                            (t 
                                (format t "Invalid input. Please enter a valid integer.~%")
                            )
                        )
                    )
                )
            )
            (format t "Could not load polynomial from file.~%")
        )
    )
)