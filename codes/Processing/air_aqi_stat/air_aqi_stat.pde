import processing.pdf.*;

Table table;
int R;
int C;
int w = 2;
int h = 2;
color col = color(0, 0, 0);
int[][] colors = new int[6][3];

void setup() {
  // color0
  colors[0][0] = 0;
  colors[0][1] = 248;
  colors[0][2] = 164;
  // color1
  colors[1][0] = 243;
  colors[1][1] = 235;
  colors[1][2] = 0;
  // color2
  colors[2][0] = 114;
  colors[2][1] = 133;
  colors[2][2] = 255;
  // color3
  colors[3][0] = 216;
  colors[3][1] = 0;
  colors[3][2] = 242;
  // color4
  colors[4][0] = 255;
  colors[4][1] = 0;
  colors[4][2] = 139;
  // color5
  colors[5][0] = 255;
  colors[5][1] = 0;
  colors[5][2] = 63;
  table = loadTable("air_aqi_stat.csv");
  R = table.getRowCount();
  C = table.getColumnCount();
  // size(579 * w, 197 * h, PDF, "aqi_stat.pdf");
  size(1158, 394, PDF, "aqi_stat.pdf");
  noStroke();
}

void draw() {
  for (int i = 0; i < R; i++) {
    for (int j = 0; j < C; j++) {
      int val = table.getInt(i, j);
      calColor(val);
      rect(j * w, i * h, w, h);
    }
  }
  exit();
}

void calColor(int x) {
  if (x <= 0) {
    fill(255, 255, 255);
  }
  else if (x <= 50) {
    fill(colors[0][0],colors[0][1],colors[0][2]);
  }
  else if (x <= 100) {
    fill(colors[1][0],colors[1][1],colors[1][2]);
  }
  else if (x <= 150) {
    fill(colors[2][0],colors[2][1],colors[2][2]);
  }
  else if (x <= 200) {
    fill(colors[3][0],colors[3][1],colors[3][2]);
  }
  else if (x <= 300) {
    fill(colors[4][0],colors[4][1],colors[4][2]);
  }
  else {
    fill(colors[5][0],colors[5][1],colors[5][2]);
  }
} 