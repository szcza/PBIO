#!/usr/bin/env python3
"""
NCBI GenBank Advanced Retriever
Pobiera dane sekwencji DNA, filtruje po długości, zapisuje CSV i tworzy wykres.
"""

from Bio import Entrez, SeqIO
import pandas as pd
import matplotlib.pyplot as plt
import time


class GenBankFetcher:
    def __init__(self, email, api_key):
        Entrez.email = email
        Entrez.api_key = api_key
        Entrez.tool = 'BioScriptEx10'
        self.records = []

    def search(self, taxid):
        print(f"Searching for taxid: {taxid}")
        handle = Entrez.esearch(db="nucleotide", term=f"txid{taxid}[Organism]", usehistory="y")
        result = Entrez.read(handle)
        self.count = int(result["Count"])
        self.query_key = result["QueryKey"]
        self.webenv = result["WebEnv"]
        print(f"Found {self.count} records.")
        return self.count

    def fetch_and_filter(self, min_len, max_len, max_records=100):
        step = 100
        for start in range(0, min(self.count, max_records), step):
            print(f"Fetching records {start} to {start + step}")
            handle = Entrez.efetch(
                db="nucleotide", rettype="gb", retmode="text",
                retstart=start, retmax=step,
                webenv=self.webenv, query_key=self.query_key
            )
            records = SeqIO.parse(handle, "genbank")
            for record in records:
                length = len(record.seq)
                if min_len <= length <= max_len:
                    self.records.append({
                        "accession": record.id,
                        "length": length,
                        "description": record.description
                    })
            time.sleep(0.4)  # by nie przekroczyć limitu

    def save_csv(self, filename):
        df = pd.DataFrame(self.records)
        df.sort_values("length", ascending=False, inplace=True)
        df.to_csv(filename, index=False)
        print(f"CSV saved to {filename}")

    def save_plot(self, filename):
        df = pd.DataFrame(self.records).sort_values("length", ascending=False)
        plt.figure(figsize=(10, 6))
        plt.plot(df["accession"], df["length"], marker='o')
        plt.xticks(rotation=90, fontsize=6)
        plt.xlabel("Accession Number")
        plt.ylabel("Sequence Length")
        plt.title("GenBank Sequences by Length")
        plt.tight_layout()
        plt.savefig(filename)
        print(f"Plot saved to {filename}")


def main():
    email = input("Enter your NCBI email: ")
    api_key = input("Enter your NCBI API key: ")
    taxid = input("Enter organism taxid: ")
    min_len = int(input("Min sequence length: "))
    max_len = int(input("Max sequence length: "))

    fetcher = GenBankFetcher(email, api_key)
    count = fetcher.search(taxid)
    if count == 0:
        print("No records found.")
        return

    fetcher.fetch_and_filter(min_len, max_len, max_records=500)
    fetcher.save_csv(f"taxid_{taxid}_filtered.csv")
    fetcher.save_plot(f"taxid_{taxid}_plot.png")


if __name__ == "__main__":
    main()
