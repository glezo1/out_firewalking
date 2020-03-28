# out_firewalking
Outgoing-rules firewalking

So you've got a non-interactive web shell on a box, but seems to be a firewall in place filtering out outgoing connections, huh?
What do you do? Test your pentestmonkey's reverse shell port after port, or you just firewalk?

# clients
As dirty as they come, with as few lines of codes as possible (you might need to deploy them in, ehmmm, rudimentary ways)
They (so far: python, modern-bash, old-bash-netcat, php) just tcp-ping every tcp port

# server
Won't listen on any port. It just listens (by tcpdump) to tcp attempts to realize if the packets leaves the compromised machine (hence, not filtered by firewall)

