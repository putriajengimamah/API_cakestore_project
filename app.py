from flask import Flask, jsonify, request, session
# pip install flask_mysqldb
from flask_mysqldb import MySQL
# pip install flask_cors
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cake'
mysql = MySQL(app)

CORS(app)

@app.route('/')
def main():
    return "Selamat Datang"

@app.route('/cakestore', methods=['GET', 'POST'])
def rempah():
# Read
    if request.method == 'GET':
        try:
            # koneksi mysql
            cur = mysql.connection.cursor()
            # query untuk mengambil semua data dalam tabel
            cur.execute("SELECT * FROM cake_store")
            # fetchall mengambil semua data yang telah di query di atas, 
            # dan menyimpannya ke result
            result = cur.fetchall()
            # mengambil nama kolom dari tabel yang di query diatas (rempah)
            column_names = [i[0] for i in cur.description]
            
            # untuk membuat struktur dictionary dengan key dan value, 
            # karna result diatas hanya berupa json value tanpa ada key
            data = []
            for row in result:
                data.append(dict(zip(column_names, row)))
            
            # menutup koneksi
            cur.close()
            
            # mengembalikan return json
            return jsonify({"status": "succes", "cake_store": data})
        except Exception as e:
            return jsonify({"error": str(e)})

    elif request.method == 'POST':
        try:
            nama = request.json['nama']
            gambar = request.json['gambar']
            deskripsi = request.json['deskripsi']
            harga = request.json['harga']
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cake_store(nama, gambar, deskripsi, harga) values(%s, %s, %s, %s)", (nama, gambar, deskripsi, harga),)
            mysql.connection.commit()
            cur.close()
            
            return jsonify({'message': 'data berhasil ditambahkan'})
        except Exception as e:
            return jsonify({"error": str(e)})

# Edit
@app.route('/cakestore/edit-bloc', methods=['PUT'])
def edit_bloc():
    try:
        data = request.get_json()
        id = data['id']
        nama = data['nama']
        gambar = data['gambar']
        deskripsi = data['deskripsi']
        harga = data['harga']
            
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cake_store SET nama = %s, gambar = %s, deskripsi = %s, harga = %s WHERE id = %s", (nama, gambar, deskripsi, harga, id),)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'data berhasil diubah'})
    except Exception as e:
        return jsonify({"error": str(e)})

# Delete    
@app.route('/cakestore/<int:id>', methods=['DELETE'])
def delete_rempah(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cake_store WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": "data berhasil dihapus"})
    except Exception as e:
        return jsonify({"error": str(e)})   

if __name__ == '__main__':
    app.run(debug=True)