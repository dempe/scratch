"""
CMS DE-SynPUF Data Downloader
Downloads synthetic Medicare claims data for medical billing error detection

Save as: scripts/download_data.py
Run with: uv run python scripts/download_data.py
"""

import os
import sys
from pathlib import Path
import requests
import zipfile
from tqdm import tqdm


class CMSDataDownloader:
    """Downloads CMS DE-SynPUF synthetic claims data"""

    def __init__(self, data_dir="./data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Base URLs for CMS data
        self.cms_base = "https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads"
        self.downloads_base = "http://downloads.cms.gov/files"

    def download_file(self, url, filename):
        """Download a file with progress bar"""
        filepath = self.data_dir / filename

        # Skip if already downloaded
        if filepath.exists():
            print(f"✓ {filename} already exists, skipping...")
            return filepath

        print(f"Downloading {filename}...")
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as f, tqdm(
                total=total_size, unit="iB", unit_scale=True, desc=filename
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    pbar.update(size)

            print(f"✓ Downloaded {filename}")
            return filepath

        except requests.exceptions.RequestException as e:
            print(f"✗ Error downloading {filename}: {e}")
            return None

    def extract_zip(self, zip_path):
        """Extract a zip file"""
        if not zip_path or not zip_path.exists():
            return

        print(f"Extracting {zip_path.name}...")
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.data_dir)
            print(f"✓ Extracted {zip_path.name}")

            # Find the extracted CSV file
            csv_files = list(self.data_dir.glob("*.csv"))
            if csv_files:
                return csv_files[0]
            return None

        except Exception as e:
            print(f"✗ Error extracting {zip_path.name}: {e}")
            return None

    def download_sample(self, sample_num=1):
        """
        Download a specific sample of the CMS data

        Args:
            sample_num: Sample number (1-20)
        """
        print(f"\n{'='*60}")
        print(f"Downloading CMS DE-SynPUF Sample {sample_num}")
        print(f"{'='*60}\n")

        files_to_download = [
            # Beneficiary Summary Files (patient demographics, chronic conditions)
            {
                "url": f"{self.cms_base}/de1_0_2008_beneficiary_summary_file_sample_{sample_num}.zip",
                "filename": f"beneficiary_2008_sample_{sample_num}.zip",
                "type": "beneficiary",
            },
            {
                "url": f"{self.cms_base}/de1_0_2009_beneficiary_summary_file_sample_{sample_num}.zip",
                "filename": f"beneficiary_2009_sample_{sample_num}.zip",
                "type": "beneficiary",
            },
            {
                "url": f"https://www.cms.gov/sites/default/files/2020-09/DE1_0_2010_Beneficiary_Summary_File_Sample_{sample_num}.zip",
                "filename": f"beneficiary_2010_sample_{sample_num}.zip",
                "type": "beneficiary",
            },
            # Carrier Claims (physician/supplier services - Part B)
            {
                "url": f"{self.downloads_base}/DE1_0_2008_to_2010_Carrier_Claims_Sample_{sample_num}A.zip",
                "filename": f"carrier_claims_sample_{sample_num}A.zip",
                "type": "carrier",
            },
            {
                "url": f"{self.downloads_base}/DE1_0_2008_to_2010_Carrier_Claims_Sample_{sample_num}B.zip",
                "filename": f"carrier_claims_sample_{sample_num}B.zip",
                "type": "carrier",
            },
            # Inpatient Claims (hospital stays)
            {
                "url": f"{self.cms_base}/de1_0_2008_to_2010_inpatient_claims_sample_{sample_num}.zip",
                "filename": f"inpatient_claims_sample_{sample_num}.zip",
                "type": "inpatient",
            },
            # Outpatient Claims (hospital outpatient services)
            {
                "url": f"{self.cms_base}/de1_0_2008_to_2010_outpatient_claims_sample_{sample_num}.zip",
                "filename": f"outpatient_claims_sample_{sample_num}.zip",
                "type": "outpatient",
            },
            # Prescription Drug Events
            {
                "url": f"{self.downloads_base}/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_{sample_num}.zip",
                "filename": f"prescription_drug_sample_{sample_num}.zip",
                "type": "prescription",
            },
        ]

        downloaded_files = {}

        for file_info in files_to_download:
            filepath = self.download_file(file_info["url"], file_info["filename"])

            if filepath:
                csv_file = self.extract_zip(filepath)

                file_type = file_info["type"]
                if file_type not in downloaded_files:
                    downloaded_files[file_type] = []
                downloaded_files[file_type].append(csv_file if csv_file else filepath)

        self._print_summary(downloaded_files)
        return downloaded_files

    def download_minimal_dataset(self):
        """
        Download just the essential files for billing error detection
        (Carrier and Outpatient claims from Sample 1)
        """
        print(f"\n{'='*60}")
        print("Downloading Minimal Dataset for Error Detection")
        print("This includes Carrier and Outpatient claims (~500MB)")
        print(f"{'='*60}\n")

        essential_files = [
            # Carrier Claims (most common for billing errors)
            {
                "url": f"{self.downloads_base}/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.zip",
                "filename": "carrier_claims_sample_1A.zip",
                "type": "carrier",
            },
            {
                "url": f"{self.downloads_base}/DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.zip",
                "filename": "carrier_claims_sample_1B.zip",
                "type": "carrier",
            },
            # Outpatient Claims
            {
                "url": f"{self.cms_base}/de1_0_2008_to_2010_outpatient_claims_sample_1.zip",
                "filename": "outpatient_claims_sample_1.zip",
                "type": "outpatient",
            },
        ]

        downloaded_files = {}

        for file_info in essential_files:
            filepath = self.download_file(file_info["url"], file_info["filename"])

            if filepath:
                csv_file = self.extract_zip(filepath)

                file_type = file_info["type"]
                if file_type not in downloaded_files:
                    downloaded_files[file_type] = []
                downloaded_files[file_type].append(csv_file if csv_file else filepath)

        self._print_summary(downloaded_files)
        return downloaded_files

    def _print_summary(self, downloaded_files):
        """Print download summary"""
        print(f"\n{'='*60}")
        print("Download Complete!")
        print(f"{'='*60}")
        print(f"Data location: {self.data_dir.absolute()}")
        print(f"\nDownloaded files by type:")
        for file_type, files in downloaded_files.items():
            print(f"  {file_type}: {len(files)} file(s)")

        print(f"\n{'='*60}")
        print("Next Steps:")
        print("1. Explore the data: uv run jupyter notebook notebooks/01_data_exploration.ipynb")
        print("2. Train the model: uv run python scripts/train_model.py")
        print(f"{'='*60}")


def main():
    """Main execution"""
    print("CMS DE-SynPUF Data Downloader")
    print("=" * 60)
    print("This will download synthetic Medicare claims data")
    print("for medical billing error detection.\n")

    downloader = CMSDataDownloader()

    print("Choose download option:")
    print("1. Minimal dataset (Carrier + Outpatient claims, ~500MB) [RECOMMENDED]")
    print("2. Full Sample 1 (All claim types, ~2GB)")
    print("3. Custom sample number (1-20)")

    choice = input("\nEnter choice (1/2/3) [default: 1]: ").strip() or "1"

    try:
        if choice == "1":
            downloader.download_minimal_dataset()
        elif choice == "2":
            downloader.download_sample(sample_num=1)
        elif choice == "3":
            sample_num = int(input("Enter sample number (1-20): "))
            if 1 <= sample_num <= 20:
                downloader.download_sample(sample_num=sample_num)
            else:
                print("Invalid sample number. Must be between 1 and 20.")
                sys.exit(1)
        else:
            print("Invalid choice. Downloading minimal dataset...")
            downloader.download_minimal_dataset()

        print("\n✓ Ready to proceed with data analysis!")

    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()