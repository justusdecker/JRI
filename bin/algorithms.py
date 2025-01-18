
def bubble_sort(arr,otherArrs):

    # Outer loop to iterate through the list n times
    
    for n in range(len(arr) - 1, 0, -1):

        # Inner loop to compare adjacent elements
        for i in range(n):
            if arr[i] > arr[i + 1]:

                # Swap elements if they are in the wrong order
                swapped = True
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                for x in otherArrs:
                    x[i], x[i + 1] = x[i + 1], x[i]
    return
    