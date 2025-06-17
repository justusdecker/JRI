# Welcome to the JRI WIKI

[YOU NEED THIS](#you-need-the-following-libs-installed)


# You need the following libs installed

> [NOTE]
>  some librarys may be added in the future!

- flask
- moviepy
- obsws-python
- colorsys
- pygame-ce

# Lets Play File

> This class contains the recording data & lets play information.

## Propertys

### episodes

This property iterates through the 'episodes'
`data` dictionary and converts each entry into an `Episode` object.

> Returns:
>
> list[Episode]: A list containing `Episode` objects, each initialized
> with data from the corresponding entry in `self.data['episodes']`.

### episode_count

> Returns the length of self.data['episodes']

### episode_length

#### set

This setter updates the 'episode_length' entry within the instance's
    `data` dictionary with the provided integer value.

> Args:
> value (int): The integer value to set as the episode length.

#### get

> Returns self.data['episodeLength']

### game_name

#### set

This setter updates the 'gameName' entry within the instance's
    `data` dictionary with the provided string value.

> Args:
> value (str): The string value to set as the game name.

#### get

> Returns self.data['gameName']

### title_ending

Title ending is used for yt uploads.

> [NOTE] `self.data['episode']['title']` + `self.data`['titleEnding']`

#### set

This setter updates the 'gameName' entry within the instance's
    `data` dictionary with the provided string value.

> Args:
> value (str): The string value to set as the game name.

#### get

> Returns self.data['gameName']

### description

Description is used for yt uploads.

#### set

This setter updates the 'description' entry within the instance's
    `data` dictionary with the provided string value.

> Args:
> value (str): The string value to set as the description.

#### get

> Returns self.data['description']