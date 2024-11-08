(defun polynomial (filename);Define the function
    (with-open-file (stream "/etc/passwd")
    (loop for line = (read-line stream nil 'foo)
        until (eq line 'foo)
        do (print line))
    )
)