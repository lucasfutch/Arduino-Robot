class A:
    def __init__(self):
        self.number = 0

class B:
    def __init__(self, instance_of_a):
        self.instance_of_a = instance_of_a

if __name__ == '__main__':
    instance_of_a = A()
    instance_of_b = B(instance_of_a)

    instance_of_b.instance_of_a.number = 5

    if (instance_of_a.number == instance_of_b.instance_of_a.number):
        print "Passed by reference"
    else:
        print "Passed value :("
