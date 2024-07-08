import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

const SkeletonLoader: React.FC = () => {
  return (
    <div className="p-4">
      <div className="flex justify-start items-center gap-4 mb-4">
        <Skeleton circle={true} height={92} width={92} />
        <div className="flex-1">
          <Skeleton height={36} width="75%" />
        </div>
      </div>
      <Skeleton height={20} width="50%" className="mb-4" />
      <hr className="w-full h-[1px] bg-gray-200 opacity-60 mb-4" />
      <div className="space-y-4">
        <Skeleton height={20} width="100%" />
        <Skeleton height={20} width="100%" />
        <Skeleton height={20} width="100%" />
        <Skeleton height={20} width="100%" />
        <Skeleton height={20} width="100%" />
      </div>
    </div>
  );
};

export default SkeletonLoader;
