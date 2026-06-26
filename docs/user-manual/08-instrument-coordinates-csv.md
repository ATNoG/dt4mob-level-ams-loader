## Instrument Coordinates CSV

The loader requires a CSV file containing instrument coordinates in ETRS89 TM06 format (EPSG:3763). Coordinates are automatically converted to WGS84 (latitude/longitude) for Ditto thing attributes.

**CSV format:**

```csv
matricula,x,y,z
A1,-77300.1234,-85100.6543,82.1234
A2,-77300.2345,-85100.5432,83.2345
I1,-77330.5678,-85130.2109,72.5678
I2,-77340.6789,-85140.1098,71.6789
```

See `instrument_coords.example.csv` in the project root for an example.
