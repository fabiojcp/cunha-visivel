-- CreateTable
CREATE TABLE `Metadata` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updatedAt` DATETIME(3) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `PdfLink` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `url` VARCHAR(191) NOT NULL,
    `hashSha512` VARCHAR(191) NOT NULL,
    `path` VARCHAR(191) NOT NULL,
    `metadataId` INTEGER NOT NULL,

    UNIQUE INDEX `PdfLink_url_key`(`url`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Page` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `number` INTEGER NOT NULL,
    `text` VARCHAR(191) NOT NULL,
    `pdfLinkId` INTEGER NOT NULL,
    `name` VARCHAR(191) NOT NULL,
    `date` VARCHAR(191) NOT NULL,
    `year` VARCHAR(191) NOT NULL,
    `edition` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `PdfLink` ADD CONSTRAINT `PdfLink_metadataId_fkey` FOREIGN KEY (`metadataId`) REFERENCES `Metadata`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Page` ADD CONSTRAINT `Page_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
