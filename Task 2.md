## Alur system 

User mengupload file pdf ke webapp, lalu webapp request presigned URL ke backend, kemudian url tersebut
digunakan untuk mengupload file pdf langsung ke S3. backend juga menyimpan beberapa metadata dan memasukannya ke 
internal database hak akses dan upload file ke S3 diatur menggunakan IAM. Pada saat mulai proses OCR setiap pengupload'an file pdf ke S3 itu adalah sebuah "Event" yang akan diteruskan oleh Eventbridge ke SQS Processing, lalu lambda function / OCR starter akan mengambil pesan dari antrean dan memanggil Textract menggunakan StartExpenseAnalysis. Selanjutnya, Ketika proses selesai, textract mengirim status dan jobId melalui SNS ke SQS Completion Queue. Lambda Result processor menerima pesan tersebut, jika berhasil lambda mengambil hasil melalui GetExpenseAnalysis, termasuk nomor invoice, tanggal, vendor dan total. di tahap Normalisasi dan validasi result processor mengirimkan hasil ekstraksi ke model LLM (AWS Bedrock) untuk membantu normalisasi, misalnya menyeragamkan format tanggal dan nilai uang. lalu di validasi lagi dan hasilnya akan disimpan ke dalam DocumentDB dalam bentuk JSON. Aplikasi eksternal bisa mengakses hasilnya melalui API Gateway dengan JWT Authorizer. API Gateway meneruskan request ke Lambda API untuk membaca data dari DocumentDB dan mengembalikan response JSON. untuk monitoring dan error handling CloudWatch mengumpulkan log dan metrik untuk memantau proses. Pesan yang gagal diproses akan di coba Kembali (retry) melalui SQS, lalu dipindahkan ke DQL jika batas percobaan tercapai. CloudWatch Alarm mengirimkan notifikasi melalui SNS Alert kepada tim operasional. 

## Alasan pemilihan services 
Amazon S3         : Menyimpan PDF sumber dan mendukung upload langsung melalui presigned URL.

IAM               : Membatasi akses setiap komponen sesuai izin yang dibutuhkan.

EventBridge       : Merutekan event upload S3 ke antrean pemrosesan.

Amazon SQS        : Menampung pekerjaan saat upload meningkat, memisahkan tahapan proses, serta mendukung retry dan DLQ.

AWS Lambda        : Menjalankan logika OCR, pengolahan hasil, dan API tanpa mengelola server.

Amazon Textract   : Menyediakan OCR dan ekstraksi field yang khusus mendukung invoice serta receipt.

Amazon SNS        : Meneruskan notifikasi penyelesaian Textract dan mendistribusikan notifikasi alarm. Keduanya memakai topic terpisah.

Amazon Bedrock    : Menyediakan akses ke LLM untuk membantu normalisasi hasil ekstraksi tanpa mengelola infrastruktur model.

Amazon DocumentDB : Menyimpan hasil ekstraksi berbentuk dokumen JSON yang dapat memiliki struktur berbeda antar-invoice.

API Gateway       : Menyediakan endpoint HTTP dan integrasi autentikasi untuk aplikasi eksternal.

CloudWatch        : Menyediakan logging, monitoring metrik, dan alarm saat terjadi masalah.