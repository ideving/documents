# Install the Go tools
If you are upgrading from an older version of Go you must first remove the existing version.

# Linux, macOS, and FreeBSD tarballs
```
tar -C /usr/local -xzvf go1.11.11.linux.tar.gz
```
(Typically these commands must be run as root or through sudo.)

Add /usr/local/go/bin to the PATH environment variable. You can do this by adding this line to your /etc/profile (for a system-wide installation) or $HOME/.profile:
```
export PATH=$PATH:/usr/local/go/bin
```

Note: changes made to a profile file may not apply until the next time you log into your computer. To apply the changes immediately, just run the shell commands directly or execute them from the profile using a command such as source $HOME/.profile.

# show go version
```
go version
```