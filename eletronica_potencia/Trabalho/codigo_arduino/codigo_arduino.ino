#define loadR1 9
#define loadR2 10
#define output_voltage 0

float reference = 0.0;
int byte_position = 0;
const int buffer_size = 5;
char reference_buffer[buffer_size];
float power = 0;

const float output_factor = 2.0/12.0;
float output;
float power_;
float sum_output = 0.0;
const int max_reads = 10;
int num_reads = 0;
int num_decimal_points = 0;
bool read_point = false;
bool started = false;

void zero_crosss_int()
{
  // Cálculo do ângulo de disparo: 60Hz-> 8.33ms (1/2 ciclo)
  // (8333us - 8.33us) / 256 = 32 (aprox)
  int powertime = int((32*(256 - power)));
  delayMicroseconds(powertime);
  digitalWrite(loadR1, HIGH);
  digitalWrite(loadR2, HIGH);
  delayMicroseconds(100);
  // Desliga o pulso
  digitalWrite(loadR1, LOW);
  digitalWrite(loadR2, LOW);
}

void read_reference()
{
  if (Serial.available())
  {
    reference_buffer[byte_position] = Serial.read();
    ++byte_position;
    
    if (byte_position == 2)
    {
      reference_buffer[byte_position] = '.';
      ++byte_position;
    }
    
    if (byte_position == buffer_size - 1)
    {
      reference_buffer[byte_position] = 0;
      reference = String(reference_buffer).toFloat();
      byte_position = 0;
      Serial.println(reference);
    }
  }
}

void read_output()
{
  sum_output += float(analogRead(output_voltage)) * (5.0 / 1024.0) / output_factor;
  num_reads++;
  if (num_reads == max_reads)
  {
    num_reads = 0;
    output = sum_output / float(max_reads);
    sum_output = 0.0;
    started = true;
  }
}

void setup()
{
  Serial.begin(9600);
  pinMode(loadR1, OUTPUT);
  pinMode(loadR2, OUTPUT);
  pinMode(output_voltage, INPUT);
  attachInterrupt(0, zero_crosss_int, RISING);
  while (Serial.available())
  {
    reference_buffer[byte_position] = Serial.read();
  }
}

void loop()
{
  read_reference();
  read_output();
  if (started)
  {
    # Controle proporcional com histerese
    if (output > reference*1.05  || output < reference*0.95)
      power_ = power - 0.1 * (output - reference);

      # Saturação
      if (power_ < 0)
        power = 0;
      else if (power_ > 135)
      {
        power = 135;
      }
      else
      {
        power = power_;
      }
  }
}
