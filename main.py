from sseclient import SSEClient

messages = SSEClient('http://blazgo.epizy.com/vm/vm.php')
for msg in messages:
    do_something_useful(msg)
