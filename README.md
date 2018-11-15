# Hand-Gesture-Recognition

***Tips***
  
1. To use matplotlib in virtualenv (mac OSX) paste following in ~/.bash_profile:

```
function frameworkpython {
    if [[ ! -z "$VIRTUAL_ENV" ]]; then
        PYTHONHOME=$VIRTUAL_ENV /usr/local/bin/python3 "$@"
    else
        /usr/local/bin/python3 "$@"
    fi
}
```

2. TensorFlow:
   - Python 3.7 does not work.
   - brew unlink python
   - Installs Python 3.6.5 - brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb


