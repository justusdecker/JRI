# New Datastructure

## Why this Structure?


### What is JFile?
JFile or for short JF(.jf) is used to have a lightweight, human readable / writable, changable format, which anyone can easy understand.

Its very simple and has typehints. So you don't have to manually update all types in python itself.

You can use lists.

> [!IMPORTANT]
> Dictionarys are currently not supported!

## How to define a Section?

### Define

> [!WARNING]
> You must define a Section to make sure your data is not mixed up at the end!
> Otherwise a `SyntaxError` will give you a lecture in `FOLLOW THE DOCUMENTATION`

```
<SECTION>
```
Thats it.

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
> Make sure you don't use `::` or `__` in your variables or sections!
### Add items to an existing list
> [!CAUTION]
> Make sure you have created a list before otherwise its raining Exceptions!


```
?A_NEW_LIST::STRING1::STRING2
```

> [!TIP]
> You can use typehints in lists as well by defining like this:
> ```
> ?A_NEW_LIST::STRING1::123$int::STRING2
> ```

### Types
- int
- float
- str(default)
> [!WARNING]
> You don't have to define str. Its defined by default.
> It will throw Exceptions at you! Don't do that!

## How to use it in Python?

# Load
```
from bin.jf_filereader import JFFileReader
FR = JFFileReader('test.jf')

# If you want to reload you file

FR.load()
```

# Save
```
from bin.jf_filereader import JFFileReader
FR = JFFileReader('test.jf')

FR.save()
```


### Get
```
from bin.jf_filereader import JFFileReader
FR = JFFileReader('test.jf')
FR.{section_title}__{variable_name}
```

> [!IMPORTANT]
> `::` does not work as a separator in Python, we use ``__``
>
> ```
> FR.SECTION__A_NEW_LIST
> ```
> will give you the new created list.

### Set
> [!IMPORTANT]
> No set method exists currently will be there ASAP!