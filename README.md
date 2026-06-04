# Portable Graphic Asset
Portable Graphic Asset (PGA) is a human readable image format. It supports a 16 x 16 resolution, with 256 colors. PGA is designed to be used for games.

# Specifications
| Section | Key Name | Value Format | Representation / Constraints | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Header** | `Name` | `["String"]` | Explicit name in quotes/brackets | Identifies the asset's title. |
| **Header** | `Author` | `["String"]` | Creator's handle in quotes/brackets | Credits the author. |
| **Header** | `Date` | `["YYYY-MM-DD"]` | ISO date format in quotes/brackets | Timestamp of creation. |
| **Payload** | `Data` | `["000, 000, ..."]` | 256 comma-separated ANSI values | Contains the 16x16 pixel grid color codes (0-255). |

# PGA Viewer
Included in this repository is a Python script, designed to be ran in a terminal. It displays a PGA's information, along with the image using ANSI escape codes.

<img width="767" height="495" alt="image" src="https://github.com/user-attachments/assets/244de885-8e74-4077-97c5-247e1cff5156" />
