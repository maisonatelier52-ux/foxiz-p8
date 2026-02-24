import React from 'react';
import { Plus } from 'lucide-react';

interface CategoryInfoProps {
    title: string;
    description: string;
}

export default function CategoryInfo({ title, description }: CategoryInfoProps) {
    return (
        <div className="pinstripe-bg py-10 mb-8">
            <div className="max-w-[1330px] mx-auto px-4 md:px-8">
                <div className="flex items-center gap-4 mb-6">
                    <h1 className="text-3xl md:text-4xl font-black category-title tracking-tight">
                        {title}
                    </h1>
                    <button className="flex items-center gap-1 px-4 py-1.5 rounded-full border border-gray-200 bg-white text-xs text-black font-bold hover:bg-gray-50 transition-colors shadow-sm mt-2">
                        <Plus size={14} className="text-gray-400" />
                        <span>Follow</span>
                    </button>
                </div>
                <p className="text-[#333333] text-md max-w-4xl leading-relaxed">
                    {description}
                </p>
            </div>
        </div>
    );
}
