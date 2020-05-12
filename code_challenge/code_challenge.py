"""
Print out all of the strings in the following array in alphabetical order, each
on a separate line. 
```
['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
```
The expected output is:
```
'Cha Cha'
'Foxtrot'
'Jive'
'Paso Doble'
'Rumba'
'Samba'
'Tango'
'Viennese Waltz'
'Waltz'
```
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process. 
"""
# Sort sort()
# Loop thru the array and print each string


def print_alph(str):
    str.sort()
    # print(str)
    for word in str:
        print(word)


# print_alph(['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot',
#             'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive'])

"""
Print out all of the strings in the following array in alphabetical order 
sorted by the _middle_ letter of each string, each on a separate line. 
If the word has an even number of letters, choose the later letter, i.e. the one closer to the end of the string.  
```
['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
```
The expected output is:
```
'Cha Cha'
'Paso Doble'
'Viennese Waltz'
'Waltz'
'Samba'
'Rumba'
'Tango'
'Foxtrot'
'Jive'
```
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process. 
"""

# Write a custom sorting criteria
#    How to get the middle letter
#       Esp. when the length is even -- get length, floor division by 2
#    How to write a function that sorts according to that letter

# Run sort with that function
# Loop and print

word = 'Tango'
print(word[len(word)//2])

# .sort(key=lambda x: x[len(x)//2])


def sort_by_mid(str):
    str.sort(key=lambda x: x[len(x)//2], reverse=True)
    # print(str)
    for word in str:
        print(word)


sort_by_mid(['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot',
             'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive'])
