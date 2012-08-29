from opening_hours import is_open

lines = open("dataset_oxfordshire_20120829").readlines()

successes = 0
failures = 0

for line in lines:
    try:
        is_open("Mo", "14:00", line)
        successes += 1
    except Exception, e:
        failures += 1
        print e

print "Successes: ", successes
print "Failures: ", failures
