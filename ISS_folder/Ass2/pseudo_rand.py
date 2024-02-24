# from datetime import datetime

# def pseudo_rand_num_gen(seed, k):
#     a = []
#     num = seed**2
#     for i in range(k):
#         count_digits = len(str(num))
#         if count_digits>4:
#             start_index = (count_digits // 2) - 2
#             num = int(str(num)[start_index:start_index+4])
#         a.append(num)
#     return a

# time_string = datetime.now().time().microsecond

# # if __name__ == "__main__":
# t = input("Enter number of random numbers: ")
# random_nums = pseudo_rand_num_gen(time_string, int(t))

# if __name__ == "__main__":
#     print("The random numbers are: ", end='')
#     output = ', '.join(map(str, random_nums))
#     print(output)



# def generate_random_point(seed):
#     x_values = pseudo_rand_num_gen(seed, 10000)
#     y_values = pseudo_rand_num_gen(seed + 2, 10000)
#     return x_values, y_values 


from datetime import datetime

def pseudo_rand_num_gen(seed, k):
    a = []
    num = seed**2
    for i in range(k):
        count_digits = len(str(num))
        if i%20 == 0:
            num = (datetime.now().time().microsecond)**2

        if count_digits>4:
            start_index = (count_digits // 2) - 2
            num = int(str(num)[start_index:start_index+4])
        a.append(num)
        num**=2
    return a

time_string = datetime.now().time().microsecond

# if _name_ == "_main_":
t = input("Enter number of random numbers: ")
random_nums = pseudo_rand_num_gen(time_string, int(t))

if __name__ == "__main__":
    print("The random numbers are: ", end='')
    output = ', '.join(map(str, random_nums))
    print(output)

def generate_random_point(seed):
    x_values = pseudo_rand_num_gen(seed, 500000)
    y_values = pseudo_rand_num_gen(seed + 2, 500000)
    return x_values, y_values
