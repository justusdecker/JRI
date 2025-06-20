# New Datastructure

## Why this Structure?


### What is JFile?
JFile or for short JF(.jf) is used to have a lightweight, human readable / writable, changable format, which anyone can easy understand.

Its very simple and has typehints. So you don't have to manually update all types in python itself.

You can use lists.

> [!CAUTION]
> Dictionarys are currently not supported!

## How to define a Variable?

### Define

```
NAME_OF_YOUR_VARIABLE = VALUE
```
> [!NOTE]
> You can use ('= ', ' =', '=', ' = ') to define a variable

> [!WARNING]
> The variable name must be python readable so don't name your vars like in this example:
> ```
> AB*C = 123
> ```

### Typehint

By writing your code like this:

```
NAME_OF_YOUR_VARIABLE$int = 123
```

Your variable will be autoconverted to int!

> [!CAUTION]
> Make sure you don't try to convert `non-numeric` values!
> This will result in a `ValueError` Exception!

### Define a list
```
%A_NEW_LIST
```

> [!NOTE]
> |Operator|Description|
> |---|---|
> |%| creates a new list
> |?| appends objects in listform to a list|
> |::|is used as a seperator|

> [!CAUTION]
> Make sure you don't use `::` in your variables!
### Add items to an existing list
> [!CAUTION]
> Make sure you have created a list before otherwise its raining Exceptions!


```
?A_NEW_LIST::STRING1::STRING2
```
### Types
- int
- float
- str(default)
