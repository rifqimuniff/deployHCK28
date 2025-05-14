# import packages
# fasapi -> package untuk membuat API
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

#FastAPI -> class untuk membuat API
app = FastAPI()

# API FUNCTION -> get, put, post, delette
# bikin key untuk akses data rahasia
api_key = 'admin28gacor'

# membuat endpoint 
# @object.function_api_type("/")
@app.get("/")
def home ():
    return {"message":"welcome to HCK 028:"}

#menjalankan API
# uvicorn nama_file_tanpa_py:name object --reload
#uvicorn main:app --reload

# http://127.0.0.1:8000

# membuat endpoint untuk membava data
@app.get("/data")
def readData():
    # baca file
    df = pd.read_csv("dataToko.csv")
    # output
    return df.to_dict(orient="records")    

@app.get("/data/{user_input}")
def searchData(user_input: int):
    # baca file
    df = pd.read_csv("dataToko.csv")

    # bikin filter
    filter = df[df["id"] == user_input]

    #bikin condition
    if len(filter) == 0:
        raise HTTPException(status_code=404, detail="Barangnya nggak adan Bro :D")
    
    # output
    return filter.to_dict(orient="records")

# bikin endpoint untuk update data
@app.post("/item/{item_name}")
def updateData(item_id: int, item_name: str, item_price: int):
    # baca file yang sudah ada
    df = pd.read_csv("dataToko.csv")

    # data tambahan
    update_data = {"id": item_id, "namaBarang": item_name, "harga": item_price}

    # convert dict to dataframe
    update_data_df = pd.DataFrame(update_data, index=[0])

    # menggabungkan data lama dengan data baru
    df = pd.concat([df, update_data_df], ignore_index=True)

    # simpan data ter-update (overwrite data lama)
    df.to_csv("dataToko.csv", index=False)

    # output
    return {"message": f"Item dengan nama {item_name} telah berhasil ditambahkan :D"}

# bikin endpoint untuk update/replace data yang sudah ada
@app.put("/update/{item_id}")
def updateData(item_id: int, item_name: str, item_price: int):
    # baca file yang sudah ada
    df = pd.read_csv("dataToko.csv")

    # data tambahan
    update_data = {"id": item_id, "namaBarang": item_name, "harga": item_price}

    # create condition to check the existing data
    if update_data["id"] not in df["id"].values:
        print("id barang tidak ada")
    else:
        # update data
        df.loc[df["id"] == update_data["id"], "namaBarang"] = update_data["namaBarang"]
        df.loc[df["id"] == update_data["id"], "harga"] = update_data["harga"]

    # simpan data ter-update (overwrite data lama)
    df.to_csv("dataToko.csv", index=False)

    # output
    return {"message": f"Item dengan nama {item_name} telah berhasil diupdate :D"}

# bikin endpoint untuk read data rahasia
@app.get("/datarahasia")
def readSecret(password: str = Header(None)):
    # baca data rahasia
    df_income = pd.read_csv("dataincome.csv")

    # kondisi untuk matching password inputan dengan api_key
    if password != api_key:
        raise HTTPException(status_code = 401, detail="Akses ditolak!")
    
    #output
    return df_income.to_dict(orient="records")