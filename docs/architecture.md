# Infinite Craft Clone Architecture Notes

## Combination storage

I'm going to store the combinations and elements in similar format that is being use for [Infinite Craft](https://neal.fun/infinite-craft/). I'm going to store the data in a JSON file called `data.json` where the elements will be stored in a dictionary and the recipes are stored in a semicolon separated string.

For the elements, they will be stored in a normalized, order-independent key dictionary. The key will be a bijective base-26 numeral system (a fancy way of I'm going to be using letters to count like a, b, c, ..., aa, ab, ...). The dictionary for each element will store an array of 4 elements:
  1) The emoji
  2) The name
  3) A number representing how many combinations or cost of crafting this element
  4) The date and time that it was discovered

So, the starting dictionary of elements will look like:

```JSON
"index": {
  "A": ["💧", "Water", 1],
  "B": ["🔥", "Fire", 1],
  "C": ["💨", "Wind", 1],
  "D": ["🌎", "Earth", 1]
}
```

For the recipes will be stored in a string of semicolon-separated recipes called `data`, where each recipe is a comma-separated list of elements. The first two elements in the recipe are the ingredients that are being combined and the third element is the resulting output element. Each new element that is formed that isn't already in the element index will be appended to the end of the list with an incremented key. So, to break it down, each element in the semicolon-separated list will follow the format of:
  1) Ingredient index
  2) Ingredient index
  3) Resulting Element index

And the `data` string will look like:

```JSON
"data": "A,B,E;B,C;F"
```

## TUI structure

TUI panes:


1. **Log/History**: (Left 20% of the terminal window from the top to the bottom of the terminal window) Scrollable list, newest log at the top, that contains the combination history (and add a symbol or something to signify when the user finds a new element AND something to signify when that is the first time that the element has been found all together). This should only be events. Some examples would be:
     * *Combination*: `{Ingredient 1} + {Ingredient 2} -> {Resulting Element}` so, for example: `Fire + Water -> Steam`
     * *Error*: If the user enters `{Ingredient 1} + {Unknown Ingredient}` it should display `{Ingredient 1} + {Unknown Ingredient} -> Error: {Unknown Ingredient} is an unknown element`
     * *No Combination*: If the user enters two ingredients that cannot be combined (the models aren't able to come up with a combination) it should display `{Ingredient 1} + {Ingredient 2} -> Unable to combine` or some message that communicates that those two ingredients aren't able to be combined
2. **Inventory**: (Right 30% of the window that stretches from the top of the terminal window to the bottom of the terminal window) Scrollabel list in alphabetical order of all elements that the user has discovered. At the top of this window it should display the stats: `Elements Found/Known Elements XX%` that tells the user the total number of elements that they've found and how many known elements there are, as well as the percentage of the known elements they've found, and `New Elements Found: XX` that tells the user how many new elements that they've found that haven't been found before. These elements should be formatted with the emoji on the left followed by the element name, for example: `🔥 Fire`.
3. **Workspace/Table**: (Center of the terminal window that fills the space between the *Log/History* and *Inventory* panes) This is the working area that will show a small set of elements that the user is currently working on. Each element should be displayed in the format with the emoji on the left followed by the name, for example `🔥 Fire`, with a border around it that has a 5px padding and rounded corners. The user should be able to click and drag the elements around as well as click and drag elements from the inventory pane into the workspace. It should detect when the user clicks and drags one element over the other by at least 75% and the user does it should try to combine the elements. The workspace should also not be fixed by the size of the workspace panel, the user should be able to scroll in the workspace to zoom in and out of the window to a certain degree and be able to click and drag to move the view of the workspace. The total "working area" of the workspace should be fixed so that the user doesn't get lost. The workspace should also contain three buttons at the top right of the screen:
    * *Clear Screen*: This should remove all of the ingredients on the screen.
    * *Organize Workspace*: This button will rearrange all of the ingredients on the workspace so that all ingredients are as far away from every other ingredient as possible. If there is only one ingredient on the workspace it should move it to the center.
    * *Recenter Workspace*: This button will reset the zoom of the workspace and reset the position of the view of the working area to the default position.


A clean TUI typically has three panes:

1. **Inventory**: list of discovered elements (left).
2. **Workbench**: two selected items and the result (center).
3. **Log/History**: recent combinations and errors (right or bottom).

**Recommended layout behavior**

- Inventory is scrollable and filterable with a search prompt.
- Workbench highlights current selection and shows the result in a large
  banner (even in a text UI this feels rewarding).
- History keeps a short list of the last 10–20 actions.

## TUI libraries

If you are in Python, `textual` is modern and good-looking. For Rust, `ratatui`
provides strong primitives with good styling. For Go, `bubbletea` + `lipgloss`
creates polished TUIs.

## Suggested interaction flow

- Use arrow keys to move in inventory.
- Press `Enter` to place into slot A, and `Tab`/`Shift+Tab` to toggle between
  slots A and B.
- Press `Space` or `Enter` on slot B to combine.
- Show the result, auto-add to inventory, and log the action.

## Validation logic

- Ensure you never create a combination where `a_id == b_id` unless you
  explicitly want self-combos.
- Keep a fast lookup map for combos in memory, even if persisted in SQLite.

