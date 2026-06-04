# Portable Graphic Asset
Portable Graphic Asset (PGA) is a human readable image format. It supports a 16 x 16 resolution, with 256 colors. PGA is designed to be used for games.

# Specifications
| Section | Key Name | Value Format | Representation / Constraints | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Header** | `Name` | `["String"]` | Explicit name in quotes/brackets | Identifies the asset's title. |
| **Header** | `Author` | `["String"]` | Creator's handle in quotes/brackets | Credits the author. |
| **Header** | `Date` | `["YYYY-MM-DD"]` | ISO date format in quotes/brackets | Timestamp of creation. |
| **Payload** | `Data` | `["000, 000, ..."]` | 256 comma-separated ANSI values | Contains the 16x16 pixel grid color codes (0-255). |
