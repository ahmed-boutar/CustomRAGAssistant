import { apiService } from './api';
import { UploadResponse } from '../types/api';

export const uploadService = {
  uploadDocument: (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    return apiService.postFormData<UploadResponse>('/upload/', formData).then(res => res.data);
  },
};